package models

type LocationTrack struct {
	tableName  struct{}  `pg:"location_track"`
	LocationId int       `pg:"location_id,pk"`
	Location   *Location `pg:"rel:has-one"`

	TrackId int    `pg:"track_id,pk"`
	Track   *Track `pg:"rel:has-one"`
}
