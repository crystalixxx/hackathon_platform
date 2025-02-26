package models

type TimelineStatus struct {
	ID       int `pg:"id,pk"`
	CountNum int `pg:"count_num,notnull"`
}
