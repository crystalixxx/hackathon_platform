package models

import "time"

type Timeline struct {
	ID          int       `pg:"id,pk"`
	Title       string    `pg:"title,type:varchar(255),notnull"`
	Description string    `pg:"description"`
	Deadline    time.Time `pg:"deadline"`
	IsBlocking  bool      `pg:"is_blocking,notnull"`

	TrackID int    `pg:"track_id"`
	Track   *Track `pg:"rel:has-one"`

	TimelineStatusID int             `pg:"timeline_status_id"`
	TimeLineStatus   *TimelineStatus `pg:"rel:has-one"`

	TimesActionStatuses []TeamActionStatus `pg:"many2many:accepted_team_action_statuses"`
}
