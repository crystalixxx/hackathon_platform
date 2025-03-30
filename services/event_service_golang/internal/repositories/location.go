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

func (r *LocationRepository) Create(tx *pg.Tx, location *models.Location) (*models.Location, error) {
	_, err := tx.Model(location).Insert()
	return location, err
}

func (r *LocationRepository) GetAllLocations(tx *pg.Tx) ([]*models.Location, error) {
	locations := make([]*models.Location, 0)
	err := tx.Model(&locations).Select()
	return locations, err
}

func (r *LocationRepository) GetLocationById(tx *pg.Tx, id int) (*models.Location, error) {
	location := new(models.Location)
	err := tx.Model(location).Where("id = ?", id).Select()
	return location, err
}

func (r *LocationRepository) Update(tx *pg.Tx, locationId int, newLocation *models.Location) (*models.Location, error) {
	location := new(models.Location)
	_, err := tx.Model(location).Set("title = ?", newLocation.Title).Where("id = ?", locationId).Returning("*").Update()
	return location, err
}

func (r *LocationRepository) ChangeLocationTitle(tx *pg.Tx, id int, title string) (*models.Location, error) {
	location := new(models.Location)
	_, err := tx.Model(location).Set("title = ?", title).Where("id = ?", id).Update()
	return location, err
}

func (r *LocationRepository) DeleteLocation(tx *pg.Tx, id int) error {
	location := &models.Location{ID: id}
	_, err := tx.Model(location).WherePK().Delete()
	return err
}
