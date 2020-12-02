// Copyright (C) 2019 Dmitry Barashev
package hellodb;

import static spark.Spark.exception;
import static spark.Spark.get;
import static spark.Spark.port;
import static spark.Spark.staticFiles;

/**
 * Это main класс приложения. Запускает Spark и вешает два обработчика запросов.
 *
 * @author dbms@barashev.net
 */
public class App {
  private final PlanetHandler planetHandler = new PlanetHandler();
  private final FlightHandler flightHandler = new FlightHandler();

  App(String dbUrl) {
    exception(Exception.class, (e, req, res) -> e.printStackTrace());
    staticFiles.location("/public");
    port(8080);

    get("/hello", (req, res) -> {
      return "Hello DB";
    });
    get("/get_planet", (req, res) -> {
      res.header("Content-type", "application/json;charset=utf-8");
      String planetId = req.queryParams("planet_id");
      if (planetId == null) {
        res.status(404);
        return "";
      } else {
        return planetHandler.getPlanet(Long.parseLong(planetId));
      }
    });
    get("/update_planet", (req, res) -> {
      res.header("Content-type", "application/json;charset=utf-8");
      String planetId = req.queryParams("planet_id");
      if (planetId == null) {
        res.status(404);
        return "";
      }
      String name = req.queryParams("name");
      planetHandler.updatePlanet(Long.parseLong(planetId), name);
      return "";
    });


    get("/planets", (req, res) -> {
      res.header("Content-type", "application/json;charset=utf-8");
      String planetId = req.queryParams("planet_id");
      return planetHandler.planets(planetId  == null ? null : Long.parseLong(planetId));
    });

    get("/flights", (req, res) -> {
      res.header("Content-type", "application/json;charset=utf-8");
      String loadCommander = req.queryParams("load_commander");
      return flightHandler.flights(loadCommander == null ? true : Boolean.valueOf(loadCommander));
    });
  }

  public static void main(String[] args) {
    new App("jdbc:postgresql://127.0.0.1:5432/postgres?user=postgres");
  }
}
