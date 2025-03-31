package schemas

type LocationTrack struct {
	LocationId int `json:"location_id" validate:"required" example:"15"`
	TrackId    int `json:"track_id" validate:"required" example:"15"`
}
