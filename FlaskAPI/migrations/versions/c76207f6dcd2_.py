"""empty message

Revision ID: c76207f6dcd2
Revises: 
Create Date: 2020-05-24 15:39:02.421661

"""
import geoalchemy2
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c76207f6dcd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
#    op.create_table('geography_columns',
#    sa.Column('f_table_catalog', sa.String(), nullable=True),
#    sa.Column('f_table_schema', sa.String(), nullable=True),
#    sa.Column('f_table_name', sa.String(), nullable=True),
#    sa.Column('f_geography_column', sa.String(), nullable=True),
#    sa.Column('coord_dimension', sa.Integer(), nullable=True),
#    sa.Column('srid', sa.Integer(), nullable=True),
#    sa.Column('type', sa.Text(), nullable=True)
#    )
#    op.create_table('geometry_columns',
#    sa.Column('f_table_catalog', sa.String(length=256), nullable=True),
#    sa.Column('f_table_schema', sa.String(), nullable=True),
#    sa.Column('f_table_name', sa.String(), nullable=True),
#    sa.Column('f_geometry_column', sa.String(), nullable=True),
#    sa.Column('coord_dimension', sa.Integer(), nullable=True),
#    sa.Column('srid', sa.Integer(), nullable=True),
#    sa.Column('type', sa.String(length=30), nullable=True)
#    )
    op.create_table('gpsapidattest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('satellites', sa.Integer(), nullable=True),
    sa.Column('altitude', sa.Float(), nullable=True),
    sa.Column('speed', sa.Float(), nullable=True),
    sa.Column('accuracy', sa.Float(), nullable=True),
    sa.Column('direction', sa.Integer(), nullable=True),
    sa.Column('provider', sa.String(length=30), nullable=True),
    sa.Column('timestamp_epoch', sa.DateTime(), nullable=True),
    sa.Column('timeutc', sa.DateTime(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('startstamp', sa.DateTime(), nullable=True),
    sa.Column('battery', sa.Integer(), nullable=True),
    sa.Column('androidid', sa.String(length=30), nullable=True),
    sa.Column('serial', sa.String(length=30), nullable=True),
    sa.Column('profile', sa.String(length=30), nullable=True),
    sa.Column('hhop', sa.Float(), nullable=True),
    sa.Column('vdop', sa.Float(), nullable=True),
    sa.Column('pdop', sa.Float(), nullable=True),
    sa.Column('activity', sa.String(length=30), nullable=True),
    sa.Column('travelled', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
#    op.create_table('raster_columns',
#    sa.Column('r_table_catalog', sa.String(), nullable=True),
#    sa.Column('r_table_schema', sa.String(), nullable=True),
#    sa.Column('r_table_name', sa.String(), nullable=True),
#    sa.Column('r_raster_column', sa.String(), nullable=True),
#    sa.Column('srid', sa.Integer(), nullable=True),
#    sa.Column('scale_x', sa.Float(precision=53), nullable=True),
#    sa.Column('scale_y', sa.Float(precision=53), nullable=True),
#    sa.Column('blocksize_x', sa.Integer(), nullable=True),
#    sa.Column('blocksize_y', sa.Integer(), nullable=True),
#    sa.Column('same_alignment', sa.Boolean(), nullable=True),
#    sa.Column('regular_blocking', sa.Boolean(), nullable=True),
#    sa.Column('num_bands', sa.Integer(), nullable=True),
#    sa.Column('pixel_types', sa.ARRAY(sa.TEXT()), nullable=True),
#    sa.Column('nodata_values', sa.ARRAY(sa.Float(precision=53)), nullable=True),
#    sa.Column('out_db', sa.Boolean(), nullable=True),
#    sa.Column('extent', geoalchemy2.types.Geometry(from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
#    sa.Column('spatial_index', sa.Boolean(), nullable=True)
#    )
#    op.create_table('raster_overviews',
#    sa.Column('o_table_catalog', sa.String(), nullable=True),
#    sa.Column('o_table_schema', sa.String(), nullable=True),
#    sa.Column('o_table_name', sa.String(), nullable=True),
#    sa.Column('o_raster_column', sa.String(), nullable=True),
#    sa.Column('r_table_catalog', sa.String(), nullable=True),
#    sa.Column('r_table_schema', sa.String(), nullable=True),
#    sa.Column('r_table_name', sa.String(), nullable=True),
#    sa.Column('r_raster_column', sa.String(), nullable=True),
#    sa.Column('overview_factor', sa.Integer(), nullable=True)
#    )
#    op.create_index(op.f('ix_All_Strava_Activities_geom'), 'All_Strava_Activities', ['geom'], unique=False)
#    op.drop_index('sidx_All_Strava_Activities_geom', table_name='All_Strava_Activities')
#    op.create_index(op.f('ix_CA_Counties_geom'), 'CA_Counties', ['geom'], unique=False)
#    op.drop_index('sidx_CA_Counties_geom', table_name='CA_Counties')
#    op.create_index(op.f('ix_California_Places_geom'), 'California_Places', ['geom'], unique=False)
#    op.drop_index('sidx_California_Places_geom', table_name='California_Places')
#    op.create_index(op.f('ix_OSM_Central_CA_Trails_geom'), 'OSM_Central_CA_Trails', ['geom'], unique=False)
#    op.drop_index('sidx_OSM_Central_CA_Trails_geom', table_name='OSM_Central_CA_Trails')
#    op.create_index(op.f('ix_POI_geom'), 'POI', ['geom'], unique=False)
#    op.drop_index('sidx_POI_geom', table_name='POI')
#    op.create_index(op.f('ix_moco_roads_geom'), 'moco_roads', ['geom'], unique=False)
#    op.drop_index('sidx_moco_roads_geom', table_name='moco_roads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
#    op.create_index('sidx_moco_roads_geom', 'moco_roads', ['geom'], unique=False)
#    op.drop_index(op.f('ix_moco_roads_geom'), table_name='moco_roads')
#    op.create_index('sidx_POI_geom', 'POI', ['geom'], unique=False)
#    op.drop_index(op.f('ix_POI_geom'), table_name='POI')
#    op.create_index('sidx_OSM_Central_CA_Trails_geom', 'OSM_Central_CA_Trails', ['geom'], unique=False)
#    op.drop_index(op.f('ix_OSM_Central_CA_Trails_geom'), table_name='OSM_Central_CA_Trails')
#    op.create_index('sidx_California_Places_geom', 'California_Places', ['geom'], unique=False)
#    op.drop_index(op.f('ix_California_Places_geom'), table_name='California_Places')
#    op.create_index('sidx_CA_Counties_geom', 'CA_Counties', ['geom'], unique=False)
#    op.drop_index(op.f('ix_CA_Counties_geom'), table_name='CA_Counties')
#    op.create_index('sidx_All_Strava_Activities_geom', 'All_Strava_Activities', ['geom'], unique=False)
#    op.drop_index(op.f('ix_All_Strava_Activities_geom'), table_name='All_Strava_Activities')
#    op.drop_table('raster_overviews')
#    op.drop_table('raster_columns')
#    op.drop_table('gpsapidattest')
#    op.drop_table('geometry_columns')
#    op.drop_table('geography_columns')
    pass
    # ### end Alembic commands ###