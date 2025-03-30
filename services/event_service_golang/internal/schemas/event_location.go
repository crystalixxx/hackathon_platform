package schemas

type EventLocation struct {
	LocationID string `json:"location_id" validate:"required" example:"15"`
	EventID    string `json:"event_id" validate:"required" example:"15"`
}
