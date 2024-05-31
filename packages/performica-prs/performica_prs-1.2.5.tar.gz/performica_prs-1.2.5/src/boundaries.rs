use crate::minmax::MinMax;
use crate::prs::PeerRankScoreData;

#[derive(Debug, Default, Clone)]
pub struct PeerRankScoreBoundaries {
    pub skill: MinMax,
    pub teamwork: MinMax,
    pub aggregate: MinMax,
}

impl PeerRankScoreBoundaries {
    pub fn new(
        min_skill: f64,
        max_skill: f64,
        min_teamwork: f64,
        max_teamwork: f64,
        min_aggregate: f64,
        max_aggregate: f64,
    ) -> Self {
        Self {
            skill: MinMax::new(min_skill, max_skill),
            teamwork: MinMax::new(min_teamwork, max_teamwork),
            aggregate: MinMax::new(min_aggregate, max_aggregate),
        }
    }

    pub fn update(&mut self, prs: &PeerRankScoreData) {
        self.skill.update(prs.skill);
        self.teamwork.update(prs.teamwork);
        self.aggregate.update(prs.aggregate);
    }
}
