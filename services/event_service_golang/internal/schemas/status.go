package schemas

type Status struct {
	Title       string `json:"title" validate:"required" example:"Status Link"`
	Description string `json:"description" validate:"required" example:"Status Description"`
}

type StatusUpdate struct {
	Title       string `json:"title" example:"Status Link"`
	Description string `json:"description" example:"Status Description"`
}
