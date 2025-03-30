package schemas

type EventLocation struct {
	LocationID int `json:"location_id" validate:"required" example:"15"`
	EventID    int `json:"event_id" validate:"required" example:"15"`
}
