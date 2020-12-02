// Copyright (C) 2019 Dmitry Barashev
package hellodb;

import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.ManyToOne;
import java.math.BigDecimal;
import java.sql.Date;

@Entity(name = "flight")
public class Flight {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  Long id;

  Date date;

  BigDecimal distance;

  @ManyToOne(fetch = FetchType.LAZY)
  Planet planet;

  @ManyToOne(fetch = FetchType.LAZY)
  Commander commander;
}
