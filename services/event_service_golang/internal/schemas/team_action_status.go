package schemas

import "time"

type TeamActionStatus struct {
	TrackTeamID   int       `json:"track_team_id" validate:"required" example:"1"`
	TimelineID    int       `json:"timeline_id" validate:"required" example:"1"`
	ResultValue   int       `json:"result_value" validate:"required" example:"600"`
	ResolutonLink string    `json:"resolution_link" validate:"required" example:"https://www.youtube.com"`
	CompletedAt   time.Time `json:"completed_at" validate:"required" example:"2020-01-01 00:00:00"`
	Notes         string    `json:"notes" validate:"required" example:"Notes"`
}
