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

func (r *EventRepository) Create(event *models.Event) error {
	_, err := r.DB.Model(event).Insert()
	return err
}

func (r *EventRepository) GetAllEvents() ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := r.DB.Model(&events).Select()
	return events, err
}

func (r *EventRepository) GetEventInDateRange(dateStart time.Time, dateEnd time.Time) ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := r.DB.Model(&events).Relation("Date").Where("date.start_date >= ? AND date.end_date <= ?", dateStart, dateEnd).Select()
	return events, err
}

func (r *EventRepository) GetEventByID(eventID int) (*models.Event, error) {
	event := new(models.Event)
	err := r.DB.Model(event).Where("id = ?", eventID).Select()
	return event, err
}

func (r *EventRepository) UpdateEventTitle(eventID int, title string) (*models.Event, error) {
	event := new(models.Event)
	_, err := r.DB.Model(event).Set("title = ?", title).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateEventDescription(eventID int, description string) (*models.Event, error) {
	event := new(models.Event)
	_, err := r.DB.Model(event).Set("description = ?", description).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateRedirectLink(eventID int, redirectLink string) (*models.Event, error) {
	event := new(models.Event)
	_, err := r.DB.Model(event).Set("redirect_link = ?", redirectLink).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) UpdateDateID(eventID int, dateID int) (*models.Event, error) {
	event := new(models.Event)
	_, err := r.DB.Model(event).Set("date_id = ?", dateID).Where("id = ?", eventID).Update()
	return event, err
}

func (r *EventRepository) DeleteEvent(eventID int) error {
	event := new(models.Event)
	_, err := r.DB.Model(event).Where("id = ?", eventID).Delete()
	return err
}
