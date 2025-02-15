package models

type StatusTrack struct {
	TrackID int    `pg:"track_id,pk"`
	Track   *Track `pg:"rel:has-one"`

	StatusID int     `pg:"status_id,pk"`
	Status   *Status `pg:"rel:has-one"`
}
