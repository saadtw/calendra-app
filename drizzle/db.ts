// Import PostgreSQL client for Docker/local PostgreSQL
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

// Import your database schema definitions (e.g., tables) from the local schema file
import * as schema from "./schema";

// Initialize the postgres client using the DATABASE_URL from your environment variables
const client = postgres(process.env.DATABASE_URL!);

// Create and export the Drizzle ORM instance, with the postgres client and schema for type-safe queries
export const db = drizzle(client, { schema });
