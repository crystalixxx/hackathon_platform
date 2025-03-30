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

func (r *EventRepository) Create(tx *pg.Tx, event *models.Event) (*models.Event, error) {
	_, err := tx.Model(event).Insert()
	return event, err
}

func (r *EventRepository) GetAllEvents(tx *pg.Tx) ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := tx.Model(&events).Relation("Date").Relation("Statuses").Select()
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

func (r *EventRepository) GetEventByStatus(tx *pg.Tx, status string) ([]*models.Event, error) {
	events := make([]*models.Event, 0)
	err := tx.Model(&events).Where("status = ?", status).Select()
	return events, err
}

func (r *EventRepository) UpdateEvent(tx *pg.Tx, eventId int, newEvent *models.Event) (*models.Event, error) {
	event := new(models.Event)
	_, err := tx.Model(event).Set("title = ?, description = ?, redirect_link = ?, date_id = ?, status = ?", newEvent.Title,
		newEvent.Description, newEvent.RedirectLink, newEvent.DateID, newEvent.Status).Where("id = ?", eventId).Returning("*").Update()
	return event, err
}

func (r *EventRepository) DeleteEvent(tx *pg.Tx, eventID int) error {
	event := new(models.Event)
	_, err := tx.Model(event).Where("id = ?", eventID).Delete()
	return err
}
