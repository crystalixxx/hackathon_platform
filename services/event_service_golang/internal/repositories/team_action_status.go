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

func (r *TeamActionStatusRepository) Create(teamActionStatus *models.TeamActionStatus) error {
	_, err := r.DB.Model(teamActionStatus).Insert()
	return err
}

func (r *TeamActionStatusRepository) GetAllTeamActionStatuses() ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := r.DB.Model(&teamActionStatuses).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTeamID(teamID int) ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := r.DB.Model(&teamActionStatuses).Where("track_team_id = ?", teamID).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTimelineID(timelineID int) ([]*models.TeamActionStatus, error) {
	teamActionStatuses := make([]*models.TeamActionStatus, 0)
	err := r.DB.Model(&teamActionStatuses).Where("timeline_id = ?", timelineID).Select()
	return teamActionStatuses, err
}

func (r *TeamActionStatusRepository) GetTeamActionStatusByTeamIDAndTimelineID(teamID, timelineID int) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	err := r.DB.Model(teamActionStatus).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Select()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusResultValue(teamID int, timelineID int, resultValue int) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := r.DB.Model(teamActionStatus).Set("result_value = ?", resultValue).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusResolutionLink(teamID int, timelineID int, resolutionLink string) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := r.DB.Model(teamActionStatus).Set("resolution_link = ?", resolutionLink).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusCompletedAt(teamID int, timelineID int, completedAt time.Time) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := r.DB.Model(teamActionStatus).Set("completed_at = ?", completedAt).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) UpdateTeamActionStatusNotes(teamID int, timelineID int, notes string) (*models.TeamActionStatus, error) {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := r.DB.Model(teamActionStatus).Set("notes = ?", notes).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Update()
	return teamActionStatus, err
}

func (r *TeamActionStatusRepository) DeleteTeamActionStatus(teamID int, timelineID int) error {
	teamActionStatus := new(models.TeamActionStatus)
	_, err := r.DB.Model(teamActionStatus).Where("track_team_id = ?", teamID).Where("timeline_id = ?", timelineID).Delete()
	return err
}
