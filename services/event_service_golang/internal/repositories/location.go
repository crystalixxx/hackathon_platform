package repositories

import (
	"event_service/internal/models"
	"github.com/go-pg/pg/v10"
)

type LocationRepository struct {
	DB *pg.DB
}

func NewLocationRepository(db *pg.DB) *LocationRepository {
	return &LocationRepository{DB: db}
}

func (r *LocationRepository) Create(location *models.Location) error {
	_, err := r.DB.Model(location).Insert()
	return err
}

func (r *LocationRepository) GetAllLocations() ([]*models.Location, error) {
	locations := make([]*models.Location, 0)
	err := r.DB.Model(&locations).Select()
	return locations, err
}

func (r *LocationRepository) GetLocationById(id int) (*models.Location, error) {
	location := new(models.Location)
	err := r.DB.Model(location).Where("id = ?", id).Select()
	return location, err
}

func (r *LocationRepository) ChangeLocationTitle(id int, title string) (*models.Location, error) {
	location := new(models.Location)
	_, err := r.DB.Model(location).Set("title = ?", title).Where("id = ?", id).Update()
	return location, err
}

func (r *LocationRepository) DeleteLocation(id int) error {
	location := &models.Location{ID: id}
	_, err := r.DB.Model(location).WherePK().Delete()
	return err
}
