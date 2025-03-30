package schemas

type StatusEvent struct {
	EventID  int `json:"event_id" validate:"required" example:"1"`
	StatusID int `json:"status" validate:"required" example:"1"`
}
