package schemas

type TrackRole struct {
	TrackID           int  `json:"track_id" validate:"required" example:"1"`
	UserID            int  `json:"user_id" validate:"required" example:"1"`
	CanViewResults    bool `json:"can_view_results" validate:"required" example:"true"`
	CanViewStatistics bool `json:"can_view_statistics" validate:"required" example:"true"`
}
