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

func (r *DateRepository) Create(tx *pg.Tx, date *models.Date) (*models.Date, error) {
	_, err := tx.Model(date).Insert()
	return date, err
}

func (r *DateRepository) GetAllDates(tx *pg.Tx) ([]*models.Date, error) {
	dates := make([]*models.Date, 0)
	err := tx.Model(&dates).Select()
	return dates, err
}

func (r *DateRepository) GetDateById(tx *pg.Tx, id int) (*models.Date, error) {
	date := new(models.Date)
	err := tx.Model(date).Where("id = ?", id).Select()
	return date, err
}

func (r *DateRepository) ChangeDateStart(tx *pg.Tx, id int, dateStart time.Time) (*models.Date, error) {
	date := new(models.Date)
	_, err := tx.Model(date).Set("date_start = ?", dateStart).Where("id = ?", id).Update()
	return date, err
}

func (r *DateRepository) ChangeDateEnd(tx *pg.Tx, id int, dateEnd time.Time) (*models.Date, error) {
	date := new(models.Date)
	_, err := tx.Model(date).Set("date_end = ?", dateEnd).Where("id = ?", id).Update()
	return date, err
}

func (r *DateRepository) DeleteDate(tx *pg.Tx, id int) error {
	date := &models.Date{ID: id}
	_, err := tx.Model(date).WherePK().Delete()
	return err
}
