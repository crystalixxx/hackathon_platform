package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
	"time"
)

type EventRepository struct {
	DB *pg.DB
}

func NewEventRepository(db *pg.DB) *EventRepository {
	return &EventRepository{DB: db}
}

func (r *EventRepository) Create(tx *pg.Tx, event *models.Event) error {
	_, err := tx.Model(event).Insert()
	return err
}

func (r *EventRepository) GetAllEvents(tx *pg.Tx) ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := tx.Model(&events).Select()
	return events, err
}

func (r *EventRepository) GetEventInDateRange(tx *pg.Tx, dateStart time.Time, dateEnd time.Time) ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := tx.Model(&events).Relation("Date").Where("date.start_date >= ? AND date.end_date <= ?", dateStart, dateEnd).Select()
	return events, err
}

func (r *EventRepository) GetEventByID(tx *pg.Tx, eventID int) (*models.Event, error) {
	event := new(models.Event)
	err := tx.Model(event).Where("id = ?", eventID).Select()
	return event, err
}

func (r *EventRepository) UpdateEventTitle(tx *pg.Tx, eventID int, title string) (*models.Event, error) {
	event := new(models.Event)
	_, err := tx.Model(event).Set("title = ?", title).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateEventDescription(tx *pg.Tx, eventID int, description string) (*models.Event, error) {
	event := new(models.Event)
	_, err := tx.Model(event).Set("description = ?", description).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateRedirectLink(tx *pg.Tx, eventID int, redirectLink string) (*models.Event, error) {
	event := new(models.Event)
	_, err := tx.Model(event).Set("redirect_link = ?", redirectLink).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateDateID(tx *pg.Tx, eventID int, dateID int) (*models.Event, error) {
	event := new(models.Event)
	_, err := tx.Model(event).Set("date_id = ?", dateID).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) DeleteEvent(tx *pg.Tx, eventID int) error {
	event := new(models.Event)
	_, err := tx.Model(event).Where("id = ?", eventID).Delete()
	return err
}
