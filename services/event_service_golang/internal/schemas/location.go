package schemas

type Location struct {
	Title string `json:"title" validate:"required" example:"Location Title"`
}