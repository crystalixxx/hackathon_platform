package schemas

type TrackWinner struct {
	TrackID     int  `json:"track_id" validate:"required" example:"1"`
	TrackTeamID int  `json:"track_team_id" validate:"required" example:"1"`
	Place       int  `json:"place" validate:"required" example:"1"`
	IsAwardee   bool `json:"is_awardee" validate:"required" example:"true"`
}
