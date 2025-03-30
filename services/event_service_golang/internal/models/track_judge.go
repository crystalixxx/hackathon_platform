package models

type TrackJudge struct {
	tableName struct{} `pg:"track_judge"`
	TrackID   int      `pg:"track_id,pk"`
	Track     *Track   `pg:"rel:has-one"`

	JudgeID int `pg:"judge_id,pk"`
}
