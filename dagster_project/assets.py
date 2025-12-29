"""
Simple Superhero Data Pipeline

INPUT:  data/input/superheroes.csv
OUTPUT: data/output/
"""

import pandas as pd
from dagster import asset, AssetExecutionContext


# ============================================
# PATHS
# ============================================
INPUT_PATH = "data/input/superheroes.csv"
OUTPUT_DIR = "data/output"


# ============================================
# ASSET 1: Load raw superhero data
# ============================================
@asset(
    group_name="raw",
    description="Load raw superhero data from CSV",
)
def raw_superheroes(context: AssetExecutionContext) -> pd.DataFrame:
    """Read the superheroes CSV file."""
    
    df = pd.read_csv(INPUT_PATH)
    
    context.log.info(f"Loaded {len(df)} superheroes")
    
    return df


# ============================================
# ASSET 2: Clean the data
# ============================================
@asset(
    group_name="cleaned",
    description="Cleaned superhero data",
)
def cleaned_superheroes(
    context: AssetExecutionContext,
    raw_superheroes: pd.DataFrame,
) -> pd.DataFrame:
    """Clean and standardize the data."""
    
    df = raw_superheroes.copy()
    
    # Standardize text
    df["superhero_name"] = df["superhero_name"].str.strip()
    df["hero_identity"] = df["hero_identity"].str.strip()
    df["city"] = df["city"].str.strip()
    
    # Save to output
    output_path = f"{OUTPUT_DIR}/cleaned_superheroes.csv"
    df.to_csv(output_path, index=False)
    
    context.log.info(f"Saved {len(df)} heroes to {output_path}")
    
    return df


# ============================================
# ASSET 3: Heroes by city
# ============================================
@asset(
    group_name="analytics",
    description="Count of superheroes by city",
)
def heroes_by_city(
    context: AssetExecutionContext,
    cleaned_superheroes: pd.DataFrame,
) -> pd.DataFrame:
    """Count heroes per city."""
    
    df = cleaned_superheroes.groupby("city").agg(
        hero_count=("id", "count")
    ).reset_index()
    
    df = df.sort_values("hero_count", ascending=False)
    
    # Save to output
    output_path = f"{OUTPUT_DIR}/heroes_by_city.csv"
    df.to_csv(output_path, index=False)
    
    context.log.info(f"Found {len(df)} cities")
    context.log.info(f"Top city: {df.iloc[0]['city']} with {df.iloc[0]['hero_count']} heroes")
    
    return df


# ============================================
# ASSET 4: Summary stats
# ============================================
@asset(
    group_name="analytics",
    description="Summary statistics",
)
def superhero_summary(
    context: AssetExecutionContext,
    cleaned_superheroes: pd.DataFrame,
    heroes_by_city: pd.DataFrame,
) -> pd.DataFrame:
    """Create summary statistics."""
    
    summary = pd.DataFrame({
        "metric": [
            "total_heroes",
            "total_cities",
            "top_city",
            "top_city_count",
        ],
        "value": [
            len(cleaned_superheroes),
            len(heroes_by_city),
            heroes_by_city.iloc[0]["city"],
            heroes_by_city.iloc[0]["hero_count"],
        ]
    })
    
    # Save to output
    output_path = f"{OUTPUT_DIR}/superhero_summary.csv"
    summary.to_csv(output_path, index=False)
    
    context.log.info(f"Summary saved to {output_path}")
    
    return summary
