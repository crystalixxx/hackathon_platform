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

func (r *StatusEventRepository) Create(tx *pg.Tx, statusEvent *models.StatusEvent) error {
	_, err := tx.Model(statusEvent).Insert()
	return err
}

func (r *StatusEventRepository) GetAllStatusEvents(tx *pg.Tx, StatusId int) ([]*models.StatusEvent, error) {
	statusEvents := make([]*models.StatusEvent, 0)
	err := tx.Model(&statusEvents).Where("status_id = ?", StatusId).Select()
	return statusEvents, err
}

func (r *StatusEventRepository) GetAllEventsStatuses(tx *pg.Tx, EventId int) ([]*models.StatusEvent, error) {
	statusEvents := make([]*models.StatusEvent, 0)
	err := tx.Model(&statusEvents).Where("event_id = ?", EventId).Select()
	return statusEvents, err
}

func (r *StatusEventRepository) DeleteStatusEvent(tx *pg.Tx, StatusId int, EventId int) error {
	statusEvent := &models.StatusEvent{StatusID: StatusId, EventID: EventId}
	_, err := tx.Model(statusEvent).WherePK().Delete()
	return err
}
