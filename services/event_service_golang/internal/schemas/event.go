package schemas

type Event struct {
	Title        string `json:"title" validate:"required" example:"Event title"`
	Description  string `json:"description" validate:"required" example:"Event description"`
	RedirectLink string `json:"redirect_link" validate:"required" example:"http://example.com"`
	CreatedAt    string `json:"created_at" validate:"required" example:"2023-01-01T00:00:00Z"`
	UpdatedAt    string `json:"updated_at" validate:"required" example:"2023-01-01T00:00:00Z"`
	DateId       int    `json:"date_id" validate:"required" example:"1"`
	Status       string `json:"status" validate:"required" example:"planned"`
}

type EventUpdate struct {
	Title        string `json:"title" example:"Event title"`
	Description  string `json:"description" example:"Event description"`
	RedirectLink string `json:"redirect_link" example:"http://example.com"`
	DateId       int    `json:"date_id" example:"1"`
	Status       string `json:"status" example:"planned"`
}
