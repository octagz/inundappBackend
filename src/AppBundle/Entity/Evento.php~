<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * Evento
 * @ORM\Entity
 */
class Evento
{
    /**
     * @var float
     */
    private $latitud;

    /**
     * @var float
     */
    private $longitud;

    /**
     * @var \DateTime
     */
    private $fecha;

    /**
     * @var string
     * @Assert\NotBlank()
     * @Assert\NotNull()
     */
    private $fenomeno;

    /**
     * @var integer
     */
    private $id;

    /**
     * @var \Doctrine\Common\Collections\Collection
     */
    private $imagen;


    /**
     * @var \Doctrine\Common\Collections\Collection
     * @Assert\Count(
     *              min = "1", 
     *              max = "8",
     *              minMessage = "No ha ingresado una afectacion valida.", 
     *              maxMessage = "Supero el limite de afectaciones para un fenomeno."
     *              )
     */
    private $nombreAfectacion;

    public function __construct()
    {
        $this->idImagen = new \Doctrine\Common\Collections\ArrayCollection();
        $this->nombreAfectacion = new \Doctrine\Common\Collections\ArrayCollection();
        
        $this->fecha = new \DateTime();
    }

    /**
     * Set latitud
     *
     * @param float $latitud
     * @return Evento
     */
    public function setLatitud($latitud)
    {
        $this->latitud = $latitud;

        return $this;
    }

    /**
     * Get latitud
     *
     * @return float 
     */
    public function getLatitud()
    {
        return $this->latitud;
    }

    /**
     * Set longitud
     *
     * @param float $longitud
     * @return Evento
     */
    public function setLongitud($longitud)
    {
        $this->longitud = $longitud;

        return $this;
    }

    /**
     * Get longitud
     *
     * @return float 
     */
    public function getLongitud()
    {
        return $this->longitud;
    }

    /**
     * Set fecha
     *
     * @param \DateTime $fecha
     * @return Evento
     */
    public function setFecha($fecha)
    {
        $this->fecha = $fecha;

        return $this;
    }

    /**
     * Get fecha
     *
     * @return \DateTime 
     */
    public function getFecha()
    {
        return $this->fecha;
    }

    /**
     * Set fenomeno
     *
     * @param string $fenomeno
     * @return Evento
     */
    public function setFenomeno($fenomeno)
    {
        $this->fenomeno = $fenomeno;

        return $this;
    }

    /**
     * Get fenomeno
     *
     * @return string 
     */
    public function getFenomeno()
    {
        return $this->fenomeno;
    }

    /**
     * Get id
     *
     * @return integer 
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Add imagen
     *
     * @param \AppBundle\Entity\Imagen $imagen
     * @return Evento
     */
    public function addImagen(\AppBundle\Entity\Imagen $imagen)
    {
        $this->imagen[] = $imagen;

        return $this;
    }

    /**
     * Remove imagen
     *
     * @param \AppBundle\Entity\Imagen $imagen
     */
    public function removeImagen(\AppBundle\Entity\Imagen $imagen)
    {
        $this->imagen->removeElement($imagen);
    }

    /**
     * Get imagen
     *
     * @return \Doctrine\Common\Collections\Collection 
     */
    public function getImagen()
    {
        return $this->imagen;
    }

    /**
     * Add nombreAfectacion
     *
     * @param \AppBundle\Entity\Afectacion $nombreAfectacion
     * @return Evento
     */
    public function addNombreAfectacion(\AppBundle\Entity\Afectacion $nombreAfectacion)
    {
        $this->nombreAfectacion[] = $nombreAfectacion;

        return $this;
    }

    /**
     * Remove nombreAfectacion
     *
     * @param \AppBundle\Entity\Afectacion $nombreAfectacion
     */
    public function removeNombreAfectacion(\AppBundle\Entity\Afectacion $nombreAfectacion)
    {
        $this->nombreAfectacion->removeElement($nombreAfectacion);
    }

    /**
     * Get nombreAfectacion
     *
     * @return \Doctrine\Common\Collections\Collection 
     */
    public function getNombreAfectacion()
    {
        return $this->nombreAfectacion;
    }
    /**
     * @var \Doctrine\Common\Collections\Collection
     */
    private $idImagen;


    /**
     * Add idImagen
     *
     * @param \AppBundle\Entity\Imagen $idImagen
     * @return Evento
     */
    public function addIdImagen(\AppBundle\Entity\Imagen $idImagen)
    {
        $this->idImagen[] = $idImagen;

        return $this;
    }

    /**
     * Remove idImagen
     *
     * @param \AppBundle\Entity\Imagen $idImagen
     */
    public function removeIdImagen(\AppBundle\Entity\Imagen $idImagen)
    {
        $this->idImagen->removeElement($idImagen);
    }

    /**
     * Get idImagen
     *
     * @return \Doctrine\Common\Collections\Collection 
     */
    public function getIdImagen()
    {
        return $this->idImagen;
    }
}
