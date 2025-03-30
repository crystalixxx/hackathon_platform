package schemas

type StatusTrack struct {
	TrackID  int `json:"track_id" validate:"required" example:"1"`
	StatusID int `json:"status" validate:"required" example:"1"`
}
