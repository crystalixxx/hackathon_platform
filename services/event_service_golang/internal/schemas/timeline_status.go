package schemas

type TimelineStatus struct {
	CountNum int `json:"count_num" validate:"required" example:"10"`
}
