// Copyright (C) 2019 Dmitry Barashev
package hellodb;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.math.BigDecimal;

/**
 * @author dbms@barashev.net
 */
@Entity(name = "planetview")
public class PlanetView {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  Long id;

  String name;

  BigDecimal avg_distance;
  Long flight_count;

}
