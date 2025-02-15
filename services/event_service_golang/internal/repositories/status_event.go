package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type StatusEventRepository struct {
	DB *pg.DB
}

func NewStatusEventRepository(db *pg.DB) *StatusEventRepository {
	return &StatusEventRepository{DB: db}
}

func (r *StatusEventRepository) Create(statusEvent *models.StatusEvent) error {
	_, err := r.DB.Model(statusEvent).Insert()
	return err
}

func (r *StatusEventRepository) GetAllStatusEvents(StatusId int) ([]*models.StatusEvent, error) {
	statusEvents := make([]*models.StatusEvent, 0)
	err := r.DB.Model(&statusEvents).Where("status_id = ?", StatusId).Select()
	return statusEvents, err
}

func (r *StatusEventRepository) GetAllEventsStatuses(EventId int) ([]*models.StatusEvent, error) {
	statusEvents := make([]*models.StatusEvent, 0)
	err := r.DB.Model(&statusEvents).Where("event_id = ?", EventId).Select()
	return statusEvents, err
}

func (r *StatusEventRepository) DeleteStatusEvent(StatusId int, EventId int) error {
	statusEvent := &models.StatusEvent{StatusID: StatusId, EventID: EventId}
	_, err := r.DB.Model(statusEvent).WherePK().Delete()
	return err
}
