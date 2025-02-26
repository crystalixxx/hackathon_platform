package models

type TrackRole struct {
	TrackID int    `pg:"track_id,pk"`
	Track   *Track `pg:"rel:has-one"`

	UserID int `pg:"user_id,pk"`

	CanViewResults    bool `pg:"can_view_results,notnull"`
	CanViewStatistics bool `pg:"can_view_statistics,notnull"`
}
