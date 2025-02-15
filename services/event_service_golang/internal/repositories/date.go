package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
	"time"
)

type DateRepository struct {
	DB *pg.DB
}

func NewDateRepository(db *pg.DB) *DateRepository {
	return &DateRepository{DB: db}
}

func (r *DateRepository) Create(date *models.Date) error {
	_, err := r.DB.Model(date).Insert()
	return err
}

func (r *DateRepository) GetAllDates() ([]*models.Date, error) {
	dates := make([]*models.Date, 0)
	err := r.DB.Model(&dates).Select()
	return dates, err
}

func (r *DateRepository) GetDateById(id int) (*models.Date, error) {
	date := new(models.Date)
	err := r.DB.Model(date).Where("id = ?", id).Select()
	return date, err
}

func (r *DateRepository) ChangeDateStart(id int, dateStart time.Time) (*models.Date, error) {
	date := new(models.Date)
	_, err := r.DB.Model(date).Set("date_start = ?", dateStart).Where("id = ?", id).Update()
	return date, err
}

func (r *DateRepository) ChangeDateEnd(id int, dateEnd time.Time) (*models.Date, error) {
	date := new(models.Date)
	_, err := r.DB.Model(date).Set("date_end = ?", dateEnd).Where("id = ?", id).Update()
	return date, err
}

func (r *DateRepository) DeleteDate(id int) error {
	date := &models.Date{ID: id}
	_, err := r.DB.Model(date).WherePK().Delete()
	return err
}
