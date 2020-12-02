// Copyright (C) 2020 BarD Software
package hellodb;

import com.grack.nanojson.JsonStringWriter;
import com.grack.nanojson.JsonWriter;
import org.hibernate.Session;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import java.util.List;

/**
 * @author dbarashev@bardsoftware.com
 */
public class FlightHandler {
  final EntityManagerFactory emf = Persistence.createEntityManagerFactory("Marsoflot");

  String flights(boolean loadCommander) {
    final EntityManager entityManager = emf.createEntityManager();
    try {
      //String query = "FROM flight";
      String query = loadCommander ? "SELECT f FROM flight f join fetch f.commander" : "FROM flight";
      List<Flight> result = entityManager.unwrap(Session.class)
          .createQuery(query, Flight.class).getResultList();
      final JsonStringWriter jsonOut = JsonWriter.string().array();
      result.forEach( f -> {
        final JsonStringWriter value = jsonOut.object()
            .value("id", f.id)
            .value("date", f.date.toString())
            .value("distance", f.distance);
        if (loadCommander) {
          value.value("commander", f.commander.name);
        }
        jsonOut.end();
      });
      jsonOut.end();
      return jsonOut.done();
    } finally {
      entityManager.close();
    }
  }
}
