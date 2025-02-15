package models

type TrackJudge struct {
	TrackID int    `pg:"track_id,pk"`
	Track   *Track `pg:"rel:has-one"`

	JudgeID int `pg:"judge_id,pk"`
}
