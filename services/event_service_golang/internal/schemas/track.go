package schemas

type Track struct {
	Title        string `json:"title" validate:"required" example:"Track Title"`
	Description  string `json:"description" validate:"required" example:"Track Description"`
	IsScoreBased bool   `json:"is_score_based" validate:"required" example:"false"`
	EventID      int    `json:"event_id" validate:"required" example:"42"`
	DateID       int    `json:"date_id" validate:"required" example:"42"`
}

type TrackUpdate struct {
	Title        string `json:"title" example:"Track Title"`
	Description  string `json:"description" example:"Track Description"`
	IsScoreBased string `json:"is_score_based" example:"false"`
	EventID      int    `json:"event_id" example:"42"`
	DateID       int    `json:"date_id" example:"42"`
}
