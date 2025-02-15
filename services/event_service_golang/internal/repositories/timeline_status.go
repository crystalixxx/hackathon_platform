package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type TimelineStatusRepository struct {
	DB *pg.DB
}

func NewTimelineStatusRepository(db *pg.DB) *TimelineStatusRepository {
	return &TimelineStatusRepository{DB: db}
}

func (r *TimelineStatusRepository) Create(timelineStatus *models.TimelineStatus) error {
	_, err := r.DB.Model(timelineStatus).Insert()
	return err
}

func (r *TimelineStatusRepository) GetAllTimelineStatuses() ([]*models.TimelineStatus, error) {
	timelineStatuses := make([]*models.TimelineStatus, 0)
	err := r.DB.Model(&timelineStatuses).Select()
	return timelineStatuses, err
}

func (r *TimelineStatusRepository) DeleteTimelineStatus(ID int) error {
	timelineStatus := &models.TimelineStatus{ID: ID}
	_, err := r.DB.Model(timelineStatus).WherePK().Delete()
	return err
}
