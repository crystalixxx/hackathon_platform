package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type EventPrizeRepository struct {
	DB *pg.DB
}

func NewEventPrizeRepository(db *pg.DB) *EventPrizeRepository {
	return &EventPrizeRepository{DB: db}
}

func (r *EventPrizeRepository) Create(eventPrize *models.EventPrize) error {
	_, err := r.DB.Model(eventPrize).Insert()
	return err
}

func (r *EventPrizeRepository) GetAllEventPrizes() ([]*models.EventPrize, error) {
	eventPrizes := make([]*models.EventPrize, 0)
	err := r.DB.Model(&eventPrizes).Select()
	return eventPrizes, err
}

func (r *EventPrizeRepository) GetEventPrizesByEventID(eventID int) ([]*models.EventPrize, error) {
	eventPrizes := make([]*models.EventPrize, 0)
	err := r.DB.Model(&eventPrizes).Where("event_id = ?", eventID).Select()
	return eventPrizes, err
}

func (r *EventPrizeRepository) GetEventPrizeByID(eventPrizeID int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	err := r.DB.Model(eventPrize).Where("id = ?", eventPrizeID).Select()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizePlace(eventPrizeID int, place int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Set("place = ?", place).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizePrimaryPrize(eventPrizeID int, primaryPrize string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Set("primary_prize = ?", primaryPrize).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeDescription(eventPrizeID int, description string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Set("description = ?", description).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeIconURL(eventPrizeID int, iconURL string) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Set("icon_url = ?", iconURL).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) UpdateEventPrizeEventID(eventPrizeID, eventID int) (*models.EventPrize, error) {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Set("event_id = ?", eventID).Where("id = ?", eventPrizeID).Update()
	return eventPrize, err
}

func (r *EventPrizeRepository) DeleteEventPrize(eventPrizeID int) error {
	eventPrize := new(models.EventPrize)
	_, err := r.DB.Model(eventPrize).Where("id = ?", eventPrizeID).Delete()
	return err
}
