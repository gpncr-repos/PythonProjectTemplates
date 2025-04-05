CREATE TABLE well (
	id uuid NOT NULL,
	"name" varchar NOT NULL,
	radius float4 NOT NULL,
	cluster_id uuid NOT NULL,
	CONSTRAINT well_pk PRIMARY KEY (id)
);

ALTER TABLE well ADD CONSTRAINT well_cluster_fk FOREIGN KEY (cluster_id) REFERENCES cluster(id) ON DELETE CASCADE;