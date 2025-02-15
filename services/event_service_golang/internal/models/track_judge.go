package models

type TrackJudge struct {
	TrackID int    `pg:"track_id,pk"`
	Track   *Track `pg:"rel:has-one"`

	TrackJudgeID int `pg:"track_judge_id,pk"`
}
