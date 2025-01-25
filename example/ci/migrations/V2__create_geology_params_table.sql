CREATE TABLE geology_params (
	id uuid NOT NULL,
	permeability float4 NOT NULL,
	thickness float4 NOT NULL,
	layer_pressure float4 NOT NULL,
	supply_contour_radius float4 NOT NULL,
	oil_viscosity float4 NOT NULL,
	dt timestamp NOT NULL,
	cluster_id uuid NOT NULL,
	CONSTRAINT geology_params_pk PRIMARY KEY (id)
);

ALTER TABLE geology_params ADD CONSTRAINT geology_params_cluster_fk FOREIGN KEY (cluster_id) REFERENCES cluster(id) ON DELETE CASCADE;