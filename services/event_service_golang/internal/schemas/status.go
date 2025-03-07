package schemas

type Status struct {
	Title       string `json:"title" validate:"required" example:"Status Link"`
	Description string `json:"description" validate:"required" example:"Status Description"`
}
