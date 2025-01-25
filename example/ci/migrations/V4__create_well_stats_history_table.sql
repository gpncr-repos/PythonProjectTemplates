CREATE TABLE well_stats_history (
	id uuid NOT NULL,
	dt timestamp NOT NULL,
	wellbore_pressure float4 NOT NULL,
	well_id uuid NOT NULL,
	CONSTRAINT well_stats_pk PRIMARY KEY (id)
);

ALTER TABLE well_stats_history ADD CONSTRAINT well_stats_history_well_fk FOREIGN KEY (well_id) REFERENCES well(id) ON DELETE CASCADE;