// Copyright (C) 2019 Dmitry Barashev
package hellodb;

import com.grack.nanojson.JsonStringWriter;
import com.grack.nanojson.JsonWriter;
import org.hibernate.Session;

import javax.persistence.EntityManager;
import javax.persistence.EntityManagerFactory;
import javax.persistence.Persistence;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;
import java.util.Collections;
import java.util.List;
import java.util.function.Supplier;

class PlanetHandler {
  final EntityManagerFactory emf = Persistence.createEntityManagerFactory("Marsoflot");

  public PlanetHandler() {}

  void updatePlanet(Long planetId, String name) {
    final EntityManager entityManager = emf.createEntityManager();
    try {
      entityManager.getTransaction().begin();
      final Planet planet = entityManager.find(Planet.class, planetId);
      planet.name = name;
      entityManager.persist(planet);
      entityManager.getTransaction().commit();
    } finally {
      entityManager.close();
    }
  }

  String getPlanet(Long planetId) {
    final EntityManager entityManager = emf.createEntityManager();
    try {
      final Planet planet = entityManager.find(Planet.class, planetId);
      return JsonWriter.string()
          .object().value("id", planet.id).value("name", planet.name).end()
          .done();
    } finally {
      entityManager.close();
    }
  }

  String planets(Long planetId) {
    final EntityManager entityManager = emf.createEntityManager();
    try {
//      List<PlanetView> result = (planetId != null)
//          ? Collections.singletonList(entityManager.find(PlanetView.class, planetId))
//          : entityManager.unwrap(Session.class)
//              .createQuery("FROM planetview p", PlanetView.class).getResultList();

      List<PlanetView> result = (planetId != null)
          ? Collections.singletonList(entityManager.find(PlanetView.class, planetId))
          : ((Supplier<List<PlanetView>>) () -> {
              final Session session = entityManager.unwrap(Session.class);
              CriteriaBuilder cb = session.getCriteriaBuilder();
              CriteriaQuery<PlanetView> cq = cb.createQuery(PlanetView.class);
              Root<PlanetView> rootEntry = cq.from(PlanetView.class);

              return session.createQuery(cq.select(rootEntry)).getResultList();
            }).get();


      final JsonStringWriter jsonOut = JsonWriter.string().array();
      result.forEach( p -> {
        jsonOut.object().value("id", p.id).value("name", p.name).value("distance", p.avg_distance).value("flight_count", p.flight_count).end();
      });
      jsonOut.end();
      return jsonOut.done();
    } finally {
      entityManager.close();
    }
  }
}
