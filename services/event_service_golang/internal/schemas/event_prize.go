package schemas

type EventPrize struct {
	Place        int    `json:"place" validate:"required" example:"1"`
	PrimaryPrize string `json:"primary_prize" validate:"required" example:"1"`
	Description  string `json:"description" validate:"required" example:"EventPrizeDescription"`
	IconURL      string `json:"icon_url" validate:"required" example:"EventPrizeIconURL.img"`
	EventID      int    `json:"event_id" validate:"required" example:"1"`
}
