package models

type TrackTeam struct {
	ID       int  `pg:"id,pk"`
	TeamID   int  `pg:"team_id"`
	IsActive bool `pg:"is_active"`

	TrackID int    `pg:"track_id"`
	Track   *Track `pg:"rel:has-one"`

	ActionStatuses []TeamActionStatus `pg:"many2many:accepted_team_action_statuses"`
}
