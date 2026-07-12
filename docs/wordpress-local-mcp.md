# Local WordPress + MCP setup (so Claude can build/run WP sites)

Goal: a local WordPress install on your machine that Claude Code / Claude
Desktop can drive — create pages, edit content, manage plugins — for the
Enter360 rebuild and future client sites (The Ranch redo, etc.).

## Step 1 — Local WordPress

Two good options; pick one.

### Option A: LocalWP (easiest, GUI)

1. Download from https://localwp.com and install.
2. Create a site (e.g. `enter360-dev`). Note the site URL and admin login.

### Option B: Docker (scriptable, Claude can manage it)

```yaml
# docker-compose.yml
services:
  wordpress:
    image: wordpress:latest
    ports: ["8080:80"]
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wp
      WORDPRESS_DB_PASSWORD: wp
      WORDPRESS_DB_NAME: wp
    volumes:
      - ./wp-content:/var/www/html/wp-content
  db:
    image: mariadb:11
    environment:
      MYSQL_DATABASE: wp
      MYSQL_USER: wp
      MYSQL_PASSWORD: wp
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - db_data:/var/lib/mysql
volumes:
  db_data:
```

`docker compose up -d`, then finish install at http://localhost:8080.
The `wp-content/` bind mount means themes/plugins are ordinary files Claude
can edit directly — and they can live in a git repo.

## Step 2 — MCP connection

Use Automattic's official WordPress MCP:

1. In WP admin, install the **`wordpress-mcp`** plugin
   (github.com/Automattic/wordpress-mcp — install the release ZIP via
   Plugins → Add New → Upload).
2. In the plugin settings, enable it and generate a **JWT token**.
3. Register it with Claude Code on your local machine:

```bash
claude mcp add wordpress \
  -e WP_API_URL=http://localhost:8080 \
  -e JWT_TOKEN=<token from step 2> \
  -- npx -u @automattic/mcp-wordpress-remote
```

(For Claude Desktop, add the equivalent entry to `claude_desktop_config.json`.)

### Fallback that needs no MCP at all

Claude Code can drive WordPress through **WP-CLI** in Bash:
`wp post create`, `wp theme activate`, `wp plugin install` — LocalWP ships a
shell with wp-cli preloaded; in Docker use
`docker compose exec wordpress wp --allow-root ...` (add the cli image or
install wp-cli in the container). Often this is all you need for build work;
MCP shines for content/editorial operations against a *remote* site later.

## Step 3 — Keep the site in git

Theme + custom plugins in a repo (e.g. `enter360-site`), with the
`wp-content` bind mount pointed at the clone. Content/DB stays local; use
`wp db export` for snapshots. This is what lets cloud Claude sessions work on
theme code while local sessions run the actual site.

## Notes for the Enter360 rebuild

- The on-site AI agent (calls, scheduling) will be a separate service embedded
  in the WP theme — WP is the shell; the agent stack is its own build/buy
  decision (see the rebrand brief, open question #3).
- Same stack becomes the template for client sells: The Ranch rebuild first.
