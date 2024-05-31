use std::collections::HashMap;

use itertools::Itertools;

use crate::boundaries::PeerRankScoreBoundaries;
use crate::delta::PeerRankScoreDeltaData;
use crate::prs::PeerRankScoreData;
use crate::review::Review;
use crate::row::ExplodedRow;
use pyo3_chrono::NaiveDate as PyNaiveDate;

static TOO_CLOSE: f64 = 5.;

fn get_reviewer_weight(min_prs: f64, prs_range: f64, reviewer_prs: f64) -> f64 {
    if prs_range < f64::EPSILON {
        // give middle-of-the road weight to first reviews in type
        return 2.5;
    }
    (reviewer_prs - min_prs) / prs_range * 3. + 1.
}

fn calculate_expectation_weight(prs_range: f64, winner_prs: f64, loser_prs: f64) -> f64 {
    // figure out degree of unexpectedness of the outcome on a scale of 0 - 1
    if prs_range < f64::EPSILON {
        // middle of the road weight for when there are no expectations
        return 0.5;
    }
    let delta = (winner_prs - loser_prs).abs();
    let normalized_delta = delta / prs_range;
    if winner_prs > loser_prs {
        // expected result, how expected is it?
        if normalized_delta >= 0.5 {
            // a really really expected result
            0.01
        } else {
            // the smaller the delta, the less expected, all the way up to 0.5 if they're the same
            (0.5 - normalized_delta).max(0.01)
        }
    } else {
        // unexpected result, how unexpected is it?
        if normalized_delta >= 0.5 {
            // really really unexpected, return max score
            1.
        } else {
            0.5 + normalized_delta
        }
    }
}

fn get_expectation_weight(prs_range: f64, prs1: f64, prs2: f64, score1: f64, score2: f64) -> f64 {
    if score1 > score2 {
        calculate_expectation_weight(prs_range, prs1, prs2)
    } else {
        calculate_expectation_weight(prs_range, prs2, prs1)
    }
}

fn get_spread_weight(spread: f64, score1: f64, score2: f64) -> f64 {
    let delta = (score1 - score2).abs();
    if delta <= TOO_CLOSE {
        // this is a "draw" fow now
        // a draw results in everything remaining unchanged
        // need to revisit this
        return 0.;
    }
    if spread < f64::EPSILON {
        // middle of the road weight for when there are no expectations
        return 0.5;
    }
    delta / spread
}

#[derive(Clone)]
pub struct PeerRankCalculator {
    pub prs_by_employee_id: HashMap<u32, PeerRankScoreData>,
    pub prs_boundaries: PeerRankScoreBoundaries,
}

impl Default for PeerRankCalculator {
    fn default() -> Self {
        Self::new()
    }
}

impl PeerRankCalculator {
    pub fn new() -> Self {
        let prs_by_employee_id = HashMap::new();
        let prs_boundaries = PeerRankScoreBoundaries::default();
        Self {
            prs_by_employee_id,
            prs_boundaries,
        }
    }

    pub fn get_prs(&mut self, employee_id: u32) -> &PeerRankScoreData {
        self.prs_by_employee_id
            .entry(employee_id)
            .or_insert_with(|| PeerRankScoreData::zero(employee_id))
    }

    fn update_cache(&mut self, prs_values: &[PeerRankScoreData]) {
        for prs in prs_values.iter() {
            self.prs_boundaries.update(prs);
            self.prs_by_employee_id
                .insert(prs.to_member_id, prs.clone());
        }
    }

    fn explode_group(
        &mut self,
        reviews: &[Review],
        date: PyNaiveDate,
        cycle: PyNaiveDate,
        content_type_id: u32,
        from_member_id: u32,
    ) -> Vec<ExplodedRow> {
        let mut result: Vec<ExplodedRow> = Vec::new();
        if reviews.len() < 2 {
            return result;
        }
        let mut min_skill = reviews[0].skill;
        let mut max_skill = min_skill;
        let mut min_teamwork = reviews[0].teamwork;
        let mut max_teamwork = min_teamwork;
        let mut min_aggregate = reviews[0].aggregate;
        let mut max_aggregate = min_aggregate;
        for review in reviews.iter() {
            min_skill = min_skill.min(review.skill);
            max_skill = max_skill.max(review.skill);
            min_teamwork = min_teamwork.min(review.teamwork);
            max_teamwork = max_teamwork.max(review.teamwork);
            min_aggregate = min_aggregate.min(review.aggregate);
            max_aggregate = max_aggregate.max(review.aggregate);
        }
        let skill_spread = max_skill - min_skill;
        let teamwork_spread = max_teamwork - min_teamwork;
        let aggregate_spread = max_aggregate - min_aggregate;

        let reviewer_prs = self.get_prs(from_member_id).clone();
        let skill_prs_range = self.prs_boundaries.skill.range();
        let skill_reviewer_weight = get_reviewer_weight(
            self.prs_boundaries.skill.min_value,
            skill_prs_range,
            reviewer_prs.skill,
        );
        let teamwork_prs_range = self.prs_boundaries.teamwork.range();
        let teamwork_reviewer_weight = get_reviewer_weight(
            self.prs_boundaries.teamwork.min_value,
            teamwork_prs_range,
            reviewer_prs.teamwork,
        );
        let aggregate_prs_range = self.prs_boundaries.aggregate.range();
        let aggregate_reviewer_weight = get_reviewer_weight(
            self.prs_boundaries.aggregate.min_value,
            aggregate_prs_range,
            reviewer_prs.aggregate,
        );

        for c in reviews.iter().combinations(2) {
            let review1 = c[0];
            let review2 = c[1];
            let prs1 = self.get_prs(review1.to_member_id).clone();
            let prs2 = self.get_prs(review2.to_member_id).clone();

            let skill_expectation_weight = get_expectation_weight(
                skill_prs_range,
                prs1.skill,
                prs2.skill,
                review1.skill,
                review2.skill,
            );
            let skill_spread_weight = get_spread_weight(skill_spread, review1.skill, review2.skill);

            let teamwork_expectation_weight = get_expectation_weight(
                teamwork_prs_range,
                prs1.teamwork,
                prs2.teamwork,
                review1.teamwork,
                review2.teamwork,
            );
            let teamwork_spread_weight =
                get_spread_weight(teamwork_spread, review1.teamwork, review2.teamwork);

            let aggregate_expectation_weight = get_expectation_weight(
                aggregate_prs_range,
                prs1.aggregate,
                prs2.aggregate,
                review1.aggregate,
                review2.aggregate,
            );
            let aggregate_spread_weight =
                get_spread_weight(aggregate_spread, review1.aggregate, review2.aggregate);

            let skill_sign = if review1.skill > review2.skill {
                1.
            } else {
                -1.
            };
            let teamwork_sign = if review1.teamwork > review2.teamwork {
                1.
            } else {
                -1.
            };
            let aggregate_sign = if review1.aggregate > review2.aggregate {
                1.
            } else {
                -1.
            };

            let skill_increment =
                skill_sign * skill_reviewer_weight * skill_spread_weight * skill_expectation_weight;
            let teamwork_increment = teamwork_sign
                * teamwork_reviewer_weight
                * teamwork_spread_weight
                * teamwork_expectation_weight;
            let aggregate_increment = aggregate_sign
                * aggregate_reviewer_weight
                * aggregate_spread_weight
                * aggregate_expectation_weight;

            result.push(ExplodedRow {
                content_type_id,
                from_member_id,
                date,
                cycle,
                id_1: review1.id,
                id_2: review2.id,
                to_member_id_1: review1.to_member_id,
                to_member_id_2: review2.to_member_id,
                skill_reviewer_weight,
                skill_spread_weight,
                skill_expectation_weight,
                skill_increment,
                teamwork_reviewer_weight,
                teamwork_spread_weight,
                teamwork_expectation_weight,
                teamwork_increment,
                aggregate_reviewer_weight,
                aggregate_spread_weight,
                aggregate_expectation_weight,
                aggregate_increment,
            })
        }
        result
    }

    pub fn explode_date(&mut self, reviews: &[Review], date: PyNaiveDate) -> Vec<ExplodedRow> {
        let mut result: Vec<ExplodedRow> = Vec::new();
        if reviews.len() < 2 {
            return result;
        }
        let mut index = 0;
        let mut cycle = reviews[0].cycle;
        let mut content_type_id = reviews[0].content_type_id;
        let mut from_member_id = reviews[0].from_member_id;
        for (i, review) in reviews.iter().enumerate() {
            if cycle != review.cycle
                || content_type_id != review.content_type_id
                || from_member_id != review.from_member_id
            {
                result.extend(self.explode_group(
                    &reviews[index..i],
                    date,
                    cycle,
                    content_type_id,
                    from_member_id,
                ));
                index = i;
                cycle = review.cycle;
                content_type_id = review.content_type_id;
                from_member_id = review.from_member_id;
            }
        }
        result.extend(self.explode_group(
            &reviews[index..],
            date,
            cycle,
            content_type_id,
            from_member_id,
        ));
        result
    }

    pub fn process_date(
        &mut self,
        exploded_rows_for_date: &[ExplodedRow],
    ) -> Vec<PeerRankScoreData> {
        let deltas = Self::get_deltas(exploded_rows_for_date);
        let new_prs = self.get_new_peer_rank_scores(&deltas);
        self.update_cache(&new_prs);
        new_prs
    }

    pub fn get_deltas(exploded_rows_for_date: &[ExplodedRow]) -> Vec<PeerRankScoreDeltaData> {
        let mut deltas: HashMap<(u32, u32), PeerRankScoreDeltaData> = HashMap::new();
        for row in exploded_rows_for_date.iter() {
            let k = (row.id_1, row.to_member_id_1);
            deltas
                .entry(k)
                .and_modify(|delta| {
                    delta.skill += row.skill_increment;
                    delta.teamwork += row.teamwork_increment;
                    delta.aggregate += row.aggregate_increment;
                })
                .or_insert_with(|| PeerRankScoreDeltaData {
                    date: row.date,
                    survey_request_id: row.id_1,
                    to_member_id: row.to_member_id_1,
                    teamwork: row.teamwork_increment,
                    skill: row.skill_increment,
                    aggregate: row.aggregate_increment,
                });

            let k = (row.id_2, row.to_member_id_2);
            deltas
                .entry(k)
                .and_modify(|delta| {
                    delta.skill -= row.skill_increment;
                    delta.teamwork -= row.teamwork_increment;
                    delta.aggregate -= row.aggregate_increment;
                })
                .or_insert_with(|| PeerRankScoreDeltaData {
                    date: row.date,
                    survey_request_id: row.id_2,
                    to_member_id: row.to_member_id_2,
                    teamwork: -row.teamwork_increment,
                    skill: -row.skill_increment,
                    aggregate: -row.aggregate_increment,
                });
        }
        deltas.values_mut().for_each(|d| d.massage());
        deltas.values().map(|d| d.to_owned()).collect()
    }

    pub fn get_new_peer_rank_scores(
        &mut self,
        deltas: &[PeerRankScoreDeltaData],
    ) -> Vec<PeerRankScoreData> {
        let mut new_prs: HashMap<u32, PeerRankScoreData> = HashMap::new();
        for delta in deltas.iter() {
            new_prs
                .entry(delta.to_member_id)
                .and_modify(|prs| {
                    prs.skill += delta.skill;
                    prs.teamwork += delta.teamwork;
                    prs.aggregate += delta.aggregate;
                    prs.deltas.push(delta.clone());
                })
                .or_insert_with(|| {
                    let previous_prs = self.get_prs(delta.to_member_id);
                    PeerRankScoreData {
                        skill: previous_prs.skill + delta.skill,
                        teamwork: previous_prs.teamwork + delta.teamwork,
                        aggregate: previous_prs.aggregate + delta.aggregate,
                        to_member_id: delta.to_member_id,
                        date: delta.date,
                        deltas: vec![delta.clone()],
                    }
                });
        }
        new_prs.values().map(|d| d.to_owned()).collect()
    }
}
