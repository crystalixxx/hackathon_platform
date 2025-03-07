package schemas

type Event struct {
	Title        string `json:"title" validate:"required" example:"Event title"`
	Description  string `json:"description" validate:"required" example:"Event description"`
	RedirectLink string `json:"redirect_link" validate:"required" example:"http://example.com"`
	CreatedAt    string `json:"created_at" validate:"required" example:"2023-01-01T00:00:00Z"`
	UpdatedAt    string `json:"updated_at" validate:"required" example:"2023-01-01T00:00:00Z"`
	DateId       int    `json:"date_id" validate:"required" example:"1"`
}
