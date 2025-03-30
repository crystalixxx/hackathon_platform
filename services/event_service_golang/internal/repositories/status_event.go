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

func (r *StatusEventRepository) Create(tx *pg.Tx, statusEvent *models.StatusEvent) (*models.StatusEvent, error) {
	_, err := tx.Model(statusEvent).Insert()
	return statusEvent, err
}

func (r *StatusEventRepository) GetAllStatusEvents(tx *pg.Tx, StatusId int) ([]*models.Event, error) {
	events := make([]*models.Event, 0)

	err := tx.Model(&events).
		Join("JOIN status_event se ON se.event_id = event.id").
		Where("se.status_id = ?", StatusId).
		Select()

	return events, err
}

func (r *StatusEventRepository) GetAllEventsStatuses(tx *pg.Tx, EventId int) ([]*models.Status, error) {
	statuses := make([]*models.Status, 0)

	err := tx.Model(&statuses).
		Join("JOIN status_event se ON se.status_id = status.id").
		Where("se.event_id = ?", EventId).
		Select()

	return statuses, err
}

func (r *StatusEventRepository) DeleteStatusEvent(tx *pg.Tx, StatusId int, EventId int) error {
	statusEvent := &models.StatusEvent{StatusID: StatusId, EventID: EventId}
	_, err := tx.Model(statusEvent).WherePK().Delete()
	return err
}
