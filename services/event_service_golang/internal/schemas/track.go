package schemas

type Track struct {
	Title        string `json:"title" valdate:"required" example:"Track Title"`
	Description  string `json:"description" validate:"required" example:"Track Description"`
	IsScoreBased bool   `json:"is_score_based" valudate:"required" example:"false"`
	EventID      int    `json:"event_id" example:"42"`
	DateID       int    `json:"date_id" example:"42"`
}
