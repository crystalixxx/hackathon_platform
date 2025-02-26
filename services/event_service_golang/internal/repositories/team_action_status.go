package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
	"time"
)

type TeamActionStatusRepository struct {
	DB *pg.DB
}

func NewAcceptedTeamActionStatusRepository(db *pg.DB) *TeamActionStatusRepository {
	return &TeamActionStatusRepository{DB: db}
}

func (r *TeamActionStatusRepository) Create(tx *pg.Tx, teamActionStatus *models.TeamActionStatus) error {
	_, err := tx.Model(teamActionStatus).Insert()
	return err
}

func (r *TeamActionStatusRepository) GetAllTeamActionStatuses(tx *pg.Tx) ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := tx.Model(&teamActionStatuses).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTeamID(tx *pg.Tx, teamID int) ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := tx.Model(&teamActionStatuses).Where("track_team_id = ?", teamID).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTimelineID(tx *pg.Tx, timelineID int) ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := tx.Model(&teamActionStatuses).Where("timeline_id = ?", timelineID).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTeamIDAndTimelineID(tx *pg.Tx, teamID, timelineID int) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	err := tx.Model(teamActionStatus).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Select()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusResultValue(tx *pg.Tx, teamID int, timelineID int, resultValue int) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := tx.Model(teamActionStatus).Set("result_value = ?", resultValue).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusResolutionLink(tx *pg.Tx, teamID int, timelineID int, resolutionLink string) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := tx.Model(teamActionStatus).Set("resolution_link = ?", resolutionLink).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusCompletedAt(tx *pg.Tx, teamID int, timelineID int, completedAt time.Time) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := tx.Model(teamActionStatus).Set("completed_at = ?", completedAt).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusNotes(tx *pg.Tx, teamID int, timelineID int, notes string) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := tx.Model(teamActionStatus).Set("notes = ?", notes).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) DeleteTeamActionStatus(tx *pg.Tx, teamID int, timelineID int) error {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := tx.Model(teamActionStatus).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Delete()
	return err
}
