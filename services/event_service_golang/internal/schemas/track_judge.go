package schemas

type TrackJudge struct {
	TrackID int `json:"track_id" validate:"required" example:"1"`
	JudgeID int `json:"judge_id" validate:"required" example:"1"`
}
