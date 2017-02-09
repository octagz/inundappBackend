<?php

namespace AppBundle\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * Afectacion
 */
class Afectacion
{
    /**
     * @var string
     */
    private $nombre;

    /**
     * @var \Doctrine\Common\Collections\Collection
     */
    private $idEvento;

    /**
     * Constructor
     */
    public function __construct()
    {
        $this->idEvento = new \Doctrine\Common\Collections\ArrayCollection();
    }

    /**
     * Get nombre
     *
     * @return string 
     */
    public function getNombre()
    {
        return $this->nombre;
    }

    /**
     * Add idEvento
     *
     * @param \AppBundle\Entity\Evento $idEvento
     * @return Afectacion
     */
    public function addIdEvento(\AppBundle\Entity\Evento $idEvento)
    {
        $this->idEvento[] = $idEvento;

        return $this;
    }

    /**
     * Remove idEvento
     *
     * @param \AppBundle\Entity\Evento $idEvento
     */
    public function removeIdEvento(\AppBundle\Entity\Evento $idEvento)
    {
        $this->idEvento->removeElement($idEvento);
    }

    /**
     * Get idEvento
     *
     * @return \Doctrine\Common\Collections\Collection 
     */
    public function getIdEvento()
    {
        return $this->idEvento;
    }
}
